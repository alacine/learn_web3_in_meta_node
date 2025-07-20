package model

import (
	"fmt"

	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Username string `gorm:"unique;not null" json:"username,omitempty"`
	Password string `gorm:"not null" json:"password,omitempty"`
	Email    string `gorm:"unique;not null" json:"email,omitempty"`
}

func (u *User) BeforeCreate(db *gorm.DB) error {
	fmt.Println("hook for before user save")
	return nil
}

type Post struct {
	gorm.Model
	Title   string `gorm:"not null" json:"title,omitempty"`
	Content string `gorm:"not null" json:"content,omitempty"`
	UserID  uint   `json:"user_id,omitempty"`
	User    User   `json:"user"`
}

type Comment struct {
	gorm.Model
	Content string `gorm:"not null" json:"content,omitempty"`
	UserID  uint   `json:"user_id,omitempty"`
	User    User   `json:"user"`
	PostID  uint   `json:"post_id,omitempty"`
	Post    Post   `json:"post"`
}
