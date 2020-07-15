package user

type User struct {
	tableName struct{} `sql:"dc.users"`
	Id        int64
	Login     string
}
