package middleware

import (
	"fmt"
	"net/http"
	"strconv"
	"strings"
	"task4/api"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt"
)

func ValidateUriID() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		idStr := ctx.Param("id")
		id, err := strconv.Atoi(idStr)
		if err != nil {
			ctx.JSON(http.StatusBadRequest, api.RespBase{
				Code: api.CodeFailed,
				Msg:  err.Error(),
			})
			ctx.Abort()
			return
		}
		if id <= 0 {
			ctx.JSON(http.StatusBadRequest, api.RespBase{
				Code: api.CodeFailed,
				Msg:  "id should greater than 0",
			})
			ctx.Abort()
			return
		}
		ctx.Set("id", uint(id))
		ctx.Next()
	}
}

func JWTAuth() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		authHeader := ctx.GetHeader("Authorization")
		if authHeader == "" {
			ctx.JSON(http.StatusUnauthorized, api.RespBase{
				Code: api.CodeFailed,
				Msg:  "Authorization header is required",
			})
			ctx.Abort()
			return
		}

		tokenParts := strings.Split(authHeader, " ")
		if len(tokenParts) != 2 || tokenParts[0] != "Bearer" {
			ctx.JSON(http.StatusUnauthorized, api.RespBase{
				Code: api.CodeFailed,
				Msg:  "Invalid authorization header format",
			})
			ctx.Abort()
			return
		}

		tokenStr := tokenParts[1]
		token, err := jwt.Parse(tokenStr, func(token *jwt.Token) (any, error) {
			// 确保签名方法是我们期望的
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return []byte("mock secrect key"), nil
		})

		if err != nil {
			ctx.JSON(http.StatusUnauthorized, api.RespBase{
				Code: api.CodeFailed,
				Msg:  "Invalid token: " + err.Error(),
			})
			ctx.Abort()
			return
		}

		if !token.Valid {
			ctx.JSON(http.StatusUnauthorized, api.RespBase{
				Code: api.CodeFailed,
				Msg:  "Token is not valid",
			})
			ctx.Abort()
			return
		}

		if claims, ok := token.Claims.(jwt.MapClaims); ok {
			// 检查过期时间
			if exp, ok := claims["exp"].(float64); ok {
				if time.Now().Unix() > int64(exp) {
					ctx.JSON(http.StatusUnauthorized, api.RespBase{
						Code: api.CodeFailed,
						Msg:  "Token has expired",
					})
					ctx.Abort()
					return
				}
			}
			
			ctx.Set("user_id", uint(claims["id"].(float64)))
			ctx.Set("username", claims["username"].(string))
		}

		ctx.Next()
	}
}
