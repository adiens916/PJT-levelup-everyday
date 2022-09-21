import { atom, selector } from 'recoil';
import { getUserId } from '../api/api';

export const userIdState = atom({
  key: 'userIdState',
  default: getUserId(),
});
