package api

import (
	"net/http"
	"task4/model"
	"task4/service"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type CommentAPI struct{}

func (u *CommentAPI) Get(ctx *gin.Context) {
	id, _ := ctx.Get("id")
	us := service.NewCommentService(service.GetDB())
	comment, err := us.Get(id.(uint))
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "query comment failed"})
		return
	}

	ctx.JSON(http.StatusOK, Resp[model.Comment]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: comment,
	})
}

func (u *CommentAPI) Create(ctx *gin.Context) {
	var comment model.Comment
	err := ctx.ShouldBindJSON(&comment)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	us := service.NewCommentService(service.GetDB())
	comment, err = us.Create(comment)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	ctx.JSON(
		http.StatusOK,
		Resp[model.Comment]{
			Code: CodeSuccess,
			Msg:  MsgSuccess,
			Data: comment,
		},
	)
}

func (u *CommentAPI) Delete(ctx *gin.Context) {
	id, _ := ctx.Get("id")
	us := service.NewCommentService(service.GetDB())
	comment := model.Comment{
		Model: gorm.Model{
			ID: id.(uint),
		},
	}

	err := us.Delete(comment)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, "query comment failed"})
		return
	}
	ctx.JSON(http.StatusOK, Resp[model.Comment]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: comment,
	})
}

func (u *CommentAPI) Update(ctx *gin.Context) {
	us := service.NewCommentService(service.GetDB())
	var comment model.Comment
	err := ctx.ShouldBindJSON(&comment)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}
	comment, err = us.Update(comment)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, RespBase{CodeFailed, err.Error()})
		return
	}
	ctx.JSON(http.StatusOK, Resp[model.Comment]{
		Code: CodeSuccess,
		Msg:  MsgSuccess,
		Data: comment,
	})
}
