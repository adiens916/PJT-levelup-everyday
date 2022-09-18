export interface SignUpResponseType {
  id: number;
}

export interface LoginResponseType {
  id: number;
  name: string;
  last_login: string;
}

export interface LogoutResponseType {
  success: boolean;
  message: string;
}
