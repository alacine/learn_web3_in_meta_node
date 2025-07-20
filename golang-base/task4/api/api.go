package api

const (
	CodeSuccess int = iota
	CodeFailed
)

const (
	MsgSuccess string = "success"
	MsgFailed  string = "failed"
)

type RespBase struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
}

type Resp[T any] struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
	Data T      `json:"data,omitempty"`
}
