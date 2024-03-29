import React from 'react';
import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import CustomAppBar from './CustomAppBar/CustomAppBar';
import CustomDrawer from './CustomDrawer/CustomDrawer';
import { logout } from 'domain/account/api';

import { useRecoilValue } from 'recoil';
import { userTokenState } from 'domain/account/state';

export default function NavBar() {
  const userToken = useRecoilValue(userTokenState);

  const menusAll = [
    {
      name: '회원가입',
      link: '/signup',
      isLoginRequired: false,
    },
    {
      name: '로그인',
      link: '/login',
      isLoginRequired: false,
    },
    {
      name: '습관 목록',
      link: '/',
      isLoginRequired: true,
    },
    {
      name: '습관 생성',
      link: '/create',
      isLoginRequired: true,
    },
    {
      name: '로그아웃',
      link: '/',
      isLoginRequired: true,
      onClick: async () => {
        await logout();
      },
    },
  ];

  const getFilteredMenus = (isLoggedIn: boolean) =>
    menusAll.filter((menu) => menu.isLoginRequired === isLoggedIn);

  const [menus, setMenus] = React.useState(
    getFilteredMenus(Boolean(userToken)),
  );

  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  React.useEffect(() => {
    setMenus(getFilteredMenus(Boolean(userToken)));
  }, [userToken]);

  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <CustomAppBar
          navItems={menus}
          handleDrawerToggle={handleDrawerToggle}
        />
        <CustomDrawer
          navItems={menus}
          mobileOpen={mobileOpen}
          handleDrawerToggle={handleDrawerToggle}
        />
      </Box>
      <Box component="main" sx={{ marginTop: '5rem' }}>
        <Outlet />
      </Box>
    </>
  );
}

export interface NavBarType {
  navItems: {
    name: string;
    link: string;
    isLoginRequired: boolean;
    onClick?: () => void;
  }[];
  handleDrawerToggle: () => void;
  mobileOpen?: boolean;
}
