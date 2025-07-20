package api

import (
	"fmt"
	"net/http"
	"task4/model"
	"task4/service"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type UserAPI struct{}

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
		Model: gorm.Model{
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
	var puser model.User
	err := ctx.ShouldBindJSON(&puser)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}

	user, err := us.Get(puser.ID)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "get user failed"})
		return
	}
	if user.Password != puser.Password {
		ctx.JSON(http.StatusUnauthorized, RespBase{
			CodeFailed,
			"login failed: username or password not correct",
		})
		return
	}

	ctx.JSON(http.StatusOK, Resp[model.User]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: user,
	})
}
