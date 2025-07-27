package service

import (
	"errors"
	"task4/model"

	"gorm.io/gorm"
)

type UserService struct {
	db *gorm.DB
}

func NewUserService(db *gorm.DB) *UserService {
	return &UserService{db: db}
}

func (us UserService) Get(id uint) (model.User, error) {
	if us.db == nil {
		return model.User{}, errors.New("database connection is not available")
	}
	var user model.User
	result := us.db.First(&user, id)
	return user, result.Error
}

func (us UserService) Create(u model.User) (model.User, error) {
	if us.db == nil {
		return model.User{}, errors.New("database connection is not available")
	}
	result := us.db.Create(&u)
	if result.Error != nil {
		return model.User{}, result.Error
	}
	return u, nil
}

func (us UserService) Delete(u model.User) error {
	if us.db == nil {
		return errors.New("database connection is not available")
	}
	result := us.db.Delete(&u)
	return result.Error
}
func (us UserService) Update(u model.User) (model.User, error) {
	if us.db == nil {
		return model.User{}, errors.New("database connection is not available")
	}

	result := us.db.Model(&u).Updates(u)

	if result.Error != nil {
		return model.User{}, result.Error
	}

	// 获取更新后的完整用户信息
	var updatedUser model.User
	result = us.db.First(&updatedUser, u.ID)
	return updatedUser, result.Error
}
func (us UserService) Query(u model.User) ([]model.User, error) {
	if us.db == nil {
		return []model.User{}, errors.New("database connection is not available")
	}
	var users []model.User
	result := us.db.Find(&users)
	return users, result.Error
}
