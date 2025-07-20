use practice_db;
TRUNCATE TABLE student;
TRUNCATE TABLE accounts;
TRUNCATE TABLE transactions;
insert into practice_db.accounts(id, balance) values(1, 1000);
insert into practice_db.accounts(id, balance) values(2, 1100);
insert into practice_db.accounts(id, balance) values(3, 900);
select * from accounts;

-- q1
insert into student(name, age, grade) values("张三", 20, "三年级");
select * from student where age > 18;
update student set grade = "四年级" where name = "张三";
delete from student where age < 15;

-- q2
drop procedure if exists Transfer;
delimiter //
create procedure Transfer(
    p_from_id int,
    p_to_id int,
    p_amount decimal(10, 2)
)
begin
    declare from_balance_now decimal(10, 2);
    declare exit handler for sqlexception
    begin
        rollback;
        resignal;
    end;
    start transaction;

    if p_amount <= 0 then
        signal sqlstate '45000' set message_text = "转账金额必须大于0";
    end if;
    if not exists (select 1 from accounts where id = p_from_id) then
        signal sqlstate '45000' set message_text = "源账户不存在";
    end if;
    if not exists (select 1 from accounts where id = p_to_id) then
        signal sqlstate '45000' set message_text = "目标账户不存在";
    end if;

    select balance into from_balance_now
        from accounts
        where id = p_from_id
        for update;
    if from_balance_now < p_amount then
        signal sqlstate '45000' set message_text = "余额不足";
    end if;
    update accounts set balance = balance - p_amount where id = p_from_id;
    update accounts set balance = balance + p_amount where id = p_to_id;
    insert into transactions(from_account_id, to_account_id, amount) values(p_from_id, p_to_id, p_amount);
    commit;
    select "交易完成" as SUCCESS_MSG;
end//
delimiter ;

-- fail
call Transfer(4, 2, 2000);
-- fail
call Transfer(1, 2, 2000);
-- success
call Transfer(1, 2, 500);
call Transfer(2, 3, 500);
select * from accounts;
