package api

import (
	"fmt"
	"net/http"
	"task4/model"
	"task4/service"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt"
	"golang.org/x/crypto/bcrypt"
)

type UserAPI struct{}

type LoginRequest struct {
	ID       uint   `json:"id" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func (u *UserAPI) Get(ctx *gin.Context) {
	id, _ := ctx.Get("id")
	fmt.Printf("id: %v\n", id)
	us := service.NewUserService(service.GetDB())
	user, err := us.Get(id.(uint))
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "query user failed"})
		return
	}

	ctx.JSON(http.StatusOK, Resp[model.User]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: user,
	})
}

func (u *UserAPI) Create(ctx *gin.Context) {
	var user model.User
	err := ctx.ShouldBindJSON(&user)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	bp, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}
	user.Password = string(bp)

	us := service.NewUserService(service.GetDB())
	user, err = us.Create(user)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	ctx.JSON(
		http.StatusOK,
		Resp[model.User]{
			Code: CodeSuccess,
			Msg:  MsgSuccess,
			Data: user,
		},
	)
}

func (u *UserAPI) Delete(ctx *gin.Context) {
	id, _ := ctx.Get("id")
	us := service.NewUserService(service.GetDB())
	user := model.User{
		CommonModel: model.CommonModel{
			ID: id.(uint),
		},
	}

	err := us.Delete(user)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "query user failed"})
		return
	}
	ctx.JSON(http.StatusOK, Resp[model.User]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: user,
	})
}

func (u *UserAPI) Update(ctx *gin.Context) {
	us := service.NewUserService(service.GetDB())
	var user model.User
	err := ctx.ShouldBindJSON(&user)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}

	if len(user.Password) > 0 {
		bp, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
		if err != nil {
			ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
			return
		}
		user.Password = string(bp)
	}

	user, err = us.Update(user)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}
	ctx.JSON(http.StatusOK, Resp[model.User]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: user,
	})
}

func (u *UserAPI) Login(ctx *gin.Context) {
	us := service.NewUserService(service.GetDB())
	var loginReq LoginRequest
	err := ctx.ShouldBindJSON(&loginReq)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	user, err := us.Get(loginReq.ID)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "get user failed"})
		return
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(loginReq.Password))
	if err != nil {
		ctx.JSON(http.StatusUnauthorized, RespBase{CodeFailed, "Invalid username or password"})
		return
	}

	// JWT过期时间配置（24小时）
	expirationTime := time.Now().Add(24 * time.Hour)
	
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"id":       user.ID,
		"username": user.Username,
		"iat":      time.Now().Unix(),     // 签发时间
		"exp":      expirationTime.Unix(), // 过期时间
	})
	tokenStr, err := token.SignedString([]byte("mock secrect key"))
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "generate token failed: " + err.Error()})
		return
	}

	ctx.JSON(http.StatusOK, Resp[gin.H]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: gin.H{
			"user":  user,
			"token": tokenStr,
		},
	})
}
