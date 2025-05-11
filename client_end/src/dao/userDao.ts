import axios from "axios";

export async function login(username: string, password: string) {
  return axios.post("/Login", {
    username,
    password,
  });
}

export async function Register(
  username: string,
  password: string,
  avatar_id: number,
  email: string,
  cb: () => void
) {
  try {
    const data = await axios.post("/register", {
      username,
      password,
      avatar_id,
      email,
    });
    if (data.status == 200) {
      console.log("注册成功");
      cb();
    } else {
      alert("注册失败");
    }
  } catch (error) {
    console.log("出错了");
    console.log(error);
  }
}
