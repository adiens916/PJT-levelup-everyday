export interface SignUpResponseType {
  id: number;
}

export interface LoginResponseType {
  token: string;
  user_id: number;
  name?: string;
}

export interface LogoutResponseType {
  success: boolean;
  message: string;
}
