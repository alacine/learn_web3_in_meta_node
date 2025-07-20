package middleware

import (
	"net/http"
	"strconv"
	"task4/api"

	"github.com/gin-gonic/gin"
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
