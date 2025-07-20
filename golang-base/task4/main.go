package main

import (
	"task4/api"
	"task4/middleware"
	"task4/service"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func main() {
	dsn := "practice_user:practice_password@tcp(localhost:3306)/practice_db?charset=utf8mb4&collation=utf8mb4_unicode_ci&parseTime=true&loc=Local"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	err = service.Init(db)
	if err != nil {
		panic(err)
	}

	r := gin.Default()
	g := r.Group("/api/v1")
	{
		apiUser := new(api.UserAPI)
		g.POST("/register", apiUser.Create)
		g.GET("/user/:id", middleware.ValidateUriID(), apiUser.Get)
		g.DELETE("/user/:id", middleware.ValidateUriID(), apiUser.Delete)
		g.PUT("/user", apiUser.Update)
		g.POST("/login", apiUser.Login)
	}
	{
		apiPost := new(api.PostAPI)
		g.POST("/post", apiPost.Create)
		g.DELETE("/post/:id", middleware.ValidateUriID(), apiPost.Delete)
		g.PUT("/post", apiPost.Update)
		g.GET("/post/:id", middleware.ValidateUriID(), apiPost.Get)
	}
	{
		apiComment := new(api.CommentAPI)
		g.POST("/comment", apiComment.Create)
		g.DELETE("/comment/:id", middleware.ValidateUriID(), apiComment.Delete)
		g.PUT("/comment", apiComment.Update)
		g.GET("/comment/:id", middleware.ValidateUriID(), apiComment.Get)
	}

	err = r.Run(":8000")
	if err != nil {
		panic(err)
	}
}
