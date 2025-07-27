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
		g.POST("/login", apiUser.Login)

		// Protected user routes
		protected := g.Group("/", middleware.JWTAuth())
		{
			protected.GET("/user/:id", middleware.ValidateUriID(), apiUser.Get)
			protected.DELETE("/user/:id", middleware.ValidateUriID(), apiUser.Delete)
			protected.PUT("/user", apiUser.Update)
		}
	}
	{
		apiPost := new(api.PostAPI)
		protected := g.Group("/", middleware.JWTAuth())
		{
			protected.POST("/post", apiPost.Create)
			protected.DELETE("/post/:id", middleware.ValidateUriID(), apiPost.Delete)
			protected.PUT("/post", apiPost.Update)
			protected.GET("/post/:id", middleware.ValidateUriID(), apiPost.Get)
		}
	}
	{
		apiComment := new(api.CommentAPI)
		protected := g.Group("/", middleware.JWTAuth())
		{
			protected.POST("/comment", apiComment.Create)
			protected.DELETE("/comment/:id", middleware.ValidateUriID(), apiComment.Delete)
			protected.PUT("/comment", apiComment.Update)
			protected.GET("/comment/:id", middleware.ValidateUriID(), apiComment.Get)
		}
	}

	err = r.Run(":8000")
	if err != nil {
		panic(err)
	}
}
