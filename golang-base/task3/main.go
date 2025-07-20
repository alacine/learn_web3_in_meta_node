package main

import (
	"fmt"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
)

func main() {
	db, err := sqlx.Connect("mysql", "practice_user:practice_password@tcp(localhost:3306)/practice_db?charset=utf8mb4&collation=utf8mb4_unicode_ci")
	if err != nil {
		panic(err)
	}
	empployees, err := question_1(db)
	if err != nil {
		fmt.Println("question_1 error:", err)
	} else {
		fmt.Println("所有的技术部员工如下")
		fmt.Printf("%v\n", empployees)
	}

	empployees, err = question_2(db)
	if err != nil {
		fmt.Println("question_1 error:", err)
	} else {
		fmt.Println("工资最高的员工如下")
		fmt.Printf("%v\n", empployees)
	}

	books, err := question_3(db, 40.0)
	if err != nil {
		fmt.Println("question_1 error:", err)
	} else {
		fmt.Println("价格大于 40 元的书籍如下")
		fmt.Printf("%v\n", books)
	}

	_ = db.Close()
}
