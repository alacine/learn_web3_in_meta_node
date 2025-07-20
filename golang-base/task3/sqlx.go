package main

import "github.com/jmoiron/sqlx"

type Employee struct {
	ID         int     `db:"id"`
	Name       string  `db:"name"`
	Department string  `db:"department"`
	Salary     float64 `db:"salary"`
}

type Book struct {
	ID     int     `db:"id"`
	Title  string  `db:"title"`
	Author string  `db:"author"`
	Price  float64 `db:"price"`
}

// 编写Go代码，使用Sqlx查询 employees 表中所有部门为 "技术部" 的员工信息，并将结果映射到一个自定义的 Employee 结构体切片中。
func question_1(db *sqlx.DB) ([]Employee, error) {
	schema := "select * from employees where department = '技术部'"
	var employees []Employee
	err := db.Select(&employees, schema)
	if err != nil {
		return []Employee{}, err
	}
	return employees, nil
}

// 编写Go代码，使用Sqlx查询 employees 表中工资最高的员工信息，并将结果映射到一个 Employee 结构体中。
func question_2(db *sqlx.DB) ([]Employee, error) {
	schema := "select * from employees where salary = (select max(salary) from employees)"
	var employees []Employee
	err := db.Select(&employees, schema)
	if err != nil {
		return []Employee{}, err
	}
	return employees, nil
}

// 编写Go代码，使用Sqlx执行一个复杂的查询，例如查询价格大于 40 元的书籍，并将结果映射到 Book 结构体切片中，确保类型安全。
func question_3(db *sqlx.DB, price float64) ([]Book, error) {
	schema := "select * from books where price >= ?"
	var books []Book
	err := db.Select(&books, schema, price)
	if err != nil {
		return []Book{}, err
	}
	return books, nil
}
