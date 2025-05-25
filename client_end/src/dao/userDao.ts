import axios from "axios";

export function creatAPI() {
  const api = axios.create({
    baseURL: "/",
    withCredentials: true,
  });
  return api;
}

function isEmptyObject(obj: any): boolean {
  return !(obj && typeof obj === "object" && "basic" in obj);
}

export async function GetUserInfo() {
  const api = creatAPI();
  try {
    const res = await api.get("/GetUserProfile/", {
      withCredentials: true,
    });
    if (isEmptyObject(res.data)) {
      return null;
    }
    return res.data;
  } catch (error) {
    console.error("GetUserInfo error: ", error);
  }
  return null;
}

export async function Register(
  username: string,
  password: string,
  avatar_id: number,
  email: string,
  cb: () => void
) {
  try {
    const data = await axios.post("/Register/", {
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

export async function Login(
  username: string,
  password: string,
  cb: () => void
) {
  try {
    const data = await axios.post(
      "/Login/",
      {
        username,
        password,
      },
      {
        withCredentials: true,
      }
    );
    if (data.status == 200) {
      console.log("登录成功");
      console.log(data.data);
      window.dispatchEvent(new Event("user-logged-in"));
      cb();
    } else {
      alert("登录失败");
    }
  } catch (error) {
    console.log("登录出错了");
    console.log(error);
  }
}
export async function Logout(cb: () => void) {
  const api = axios.create({
    baseURL: "/",
    withCredentials: true,
  });
  try {
    await api.post("/Logout/", {}, { withCredentials: true });
    window.dispatchEvent(new Event("user-logged-out"));
  } finally {
    cb();
  }
}
