package service

import (
	"errors"
	"task4/model"

	"gorm.io/gorm"
)

type CommentService struct {
	db *gorm.DB
}

func NewCommentService(db *gorm.DB) *CommentService {
	return &CommentService{db: db}
}

func (us CommentService) Get(id uint) (model.Comment, error) {
	if us.db == nil {
		return model.Comment{}, errors.New("database connection is not available")
	}
	var user model.Comment
	result := us.db.First(&user, id)
	return user, result.Error
}

func (us CommentService) Create(u model.Comment) (model.Comment, error) {
	if us.db == nil {
		return model.Comment{}, errors.New("database connection is not available")
	}
	result := us.db.Create(&u)
	if result.Error != nil {
		return model.Comment{}, result.Error
	}
	return u, nil
}

func (us CommentService) Delete(u model.Comment) error {
	if us.db == nil {
		return errors.New("database connection is not available")
	}
	result := us.db.Delete(&u)
	return result.Error
}
func (us CommentService) Update(u model.Comment) (model.Comment, error) {
	if us.db == nil {
		return model.Comment{}, errors.New("database connection is not available")
	}

	// 使用Updates方法只更新非零值字段，避免更新created_at等时间字段
	result := us.db.Model(&u).Updates(map[string]any{
		"content": u.Content,
		"user_id": u.UserID,
		"post_id": u.PostID,
	})

	if result.Error != nil {
		return model.Comment{}, result.Error
	}

	// 获取更新后的完整评论信息
	var updatedComment model.Comment
	result = us.db.First(&updatedComment, u.ID)
	return updatedComment, result.Error
}
func (us CommentService) Query(u model.Comment) ([]model.Comment, error) {
	if us.db == nil {
		return []model.Comment{}, errors.New("database connection is not available")
	}
	var users []model.Comment
	result := us.db.Find(&users)
	return users, result.Error
}
