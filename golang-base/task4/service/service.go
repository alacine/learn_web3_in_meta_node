package service

import (
	"task4/model"

	"gorm.io/gorm"
)

var globalDB *gorm.DB

func GetDB() *gorm.DB {
	return globalDB
}

func Init(db *gorm.DB) error {
	globalDB = db
	err := db.AutoMigrate(&model.User{}, &model.Post{}, &model.Comment{})
	return err
}
