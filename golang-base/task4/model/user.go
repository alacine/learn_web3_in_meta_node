package model

import (
	"fmt"
	"time"

	"gorm.io/gorm"
)

type CommonModel struct {
	ID        uint           `gorm:"primarykey" json:"id"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"deleted_at"`
}

type User struct {
	CommonModel
	Username string `gorm:"unique;not null" json:"username,omitempty"`
	Password string `gorm:"not null" json:"password,omitempty"`
	Email    string `gorm:"unique;not null" json:"email,omitempty" binding:"email"`
}

func (u *User) BeforeCreate(db *gorm.DB) error {
	fmt.Println("hook for before user save")
	return nil
}

type Post struct {
	CommonModel
	Title   string `gorm:"not null" json:"title,omitempty"`
	Content string `gorm:"not null" json:"content,omitempty"`
	UserID  uint   `json:"user_id,omitempty"`
	User    User   `json:"user"`
}

type Comment struct {
	CommonModel
	Content string `gorm:"not null" json:"content,omitempty"`
	UserID  uint   `json:"user_id,omitempty"`
	User    User   `json:"user"`
	PostID  uint   `json:"post_id,omitempty"`
	Post    Post   `json:"post"`
}
