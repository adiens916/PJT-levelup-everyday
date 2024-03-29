import { atom } from 'recoil';
import { getUserToken } from './api';

export const userTokenState = atom({
  key: 'userIdState',
  default: getUserToken(),
});
