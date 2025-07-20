package api

import (
	"net/http"
	"task4/model"
	"task4/service"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type PostAPI struct{}

func (u *PostAPI) Get(ctx *gin.Context) {
	id, _ := ctx.Get("id")
	us := service.NewPostService(service.GetDB())
	post, err := us.Get(id.(uint))
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "query post failed"})
		return
	}

	ctx.JSON(http.StatusOK, Resp[model.Post]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: post,
	})
}

func (u *PostAPI) Create(ctx *gin.Context) {
	var post model.Post
	err := ctx.ShouldBindJSON(&post)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	us := service.NewPostService(service.GetDB())
	post, err = us.Create(post)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	ctx.JSON(
		http.StatusOK,
		Resp[model.Post]{
			Code: CodeSuccess,
			Msg:  MsgSuccess,
			Data: post,
		},
	)
}

func (u *PostAPI) Delete(ctx *gin.Context) {
	id, _ := ctx.Get("id")
	us := service.NewPostService(service.GetDB())
	post := model.Post{
		Model: gorm.Model{
			ID: id.(uint),
		},
	}

	err := us.Delete(post)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "query post failed"})
		return
	}
	ctx.JSON(http.StatusOK, Resp[model.Post]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: post,
	})
}

func (u *PostAPI) Update(ctx *gin.Context) {
	us := service.NewPostService(service.GetDB())
	var post model.Post
	err := ctx.ShouldBindJSON(&post)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}
	post, err = us.Update(post)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}
	ctx.JSON(http.StatusOK, Resp[model.Post]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: post,
	})
}
