package service

import (
	"errors"
	"task4/model"

	"gorm.io/gorm"
)

type PostService struct {
	db *gorm.DB
}

func NewPostService(db *gorm.DB) *PostService {
	return &PostService{db: db}
}

func (us PostService) Get(id uint) (model.Post, error) {
	if us.db == nil {
		return model.Post{}, errors.New("database connection is not available")
	}
	var post model.Post
	result := us.db.First(&post, id)
	return post, result.Error
}

func (us PostService) Create(u model.Post) (model.Post, error) {
	if us.db == nil {
		return model.Post{}, errors.New("database connection is not available")
	}
	result := us.db.Create(&u)
	if result.Error != nil {
		return model.Post{}, result.Error
	}
	return u, nil
}

func (us PostService) Delete(u model.Post) error {
	if us.db == nil {
		return errors.New("database connection is not available")
	}
	result := us.db.Delete(&u)
	return result.Error
}
func (us PostService) Update(u model.Post) (model.Post, error) {
	if us.db == nil {
		return model.Post{}, errors.New("database connection is not available")
	}

	// 使用Updates方法只更新非零值字段，避免更新created_at等时间字段
	result := us.db.Model(&u).Updates(map[string]any{
		"title":   u.Title,
		"content": u.Content,
		"user_id": u.UserID,
	})

	if result.Error != nil {
		return model.Post{}, result.Error
	}

	// 获取更新后的完整文章信息
	var updatedPost model.Post
	result = us.db.First(&updatedPost, u.ID)
	return updatedPost, result.Error
}
func (us PostService) Query(u model.Post) ([]model.Post, error) {
	if us.db == nil {
		return []model.Post{}, errors.New("database connection is not available")
	}
	var posts []model.Post
	result := us.db.Find(&posts)
	return posts, result.Error
}
