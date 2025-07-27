package api

import (
	"net/http"
	"task4/model"
	"task4/service"

	"github.com/gin-gonic/gin"
)

type PostAPI struct{}

type CreatePostRequest struct {
	Title   string `json:"title" binding:"required"`
	Content string `json:"content" binding:"required"`
	UserID  uint   `json:"user_id" binding:"required"`
}

type UpdatePostRequest struct {
	ID      uint   `json:"id" binding:"required"`
	Title   string `json:"title"`
	Content string `json:"content"`
}

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
	var req CreatePostRequest
	err := ctx.ShouldBindJSON(&req)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	// 转换为Post模型
	post := model.Post{
		Title:   req.Title,
		Content: req.Content,
		UserID:  req.UserID,
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
		CommonModel: model.CommonModel{
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
	var req UpdatePostRequest
	err := ctx.ShouldBindJSON(&req)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, RespBase{CodeFailed, err.Error()})
		return
	}

	// 转换为Post模型
	post := model.Post{
		CommonModel: model.CommonModel{ID: req.ID},
		Title:       req.Title,
		Content:     req.Content,
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
