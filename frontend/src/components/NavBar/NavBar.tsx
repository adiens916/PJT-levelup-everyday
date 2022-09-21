import React from 'react';
import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import CustomAppBar from './CustomAppBar/CustomAppBar';
import CustomDrawer from './CustomDrawer/CustomDrawer';
import { getUserId, logout } from '../../api/api';

const navItems = [
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
    name: '진행 중인 습관',
    link: '/timer',
    isLoginRequired: true,
  },
  {
    name: '로그아웃',
    link: '/',
    isLoginRequired: true,
    onClick: logout,
  },
];

export default function NavBar() {
  const loggedIn = Boolean(getUserId());
  const navItemsActive = navItems.filter(
    (item) => item.isLoginRequired === loggedIn,
  );

  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <CustomAppBar
          navItems={navItemsActive}
          handleDrawerToggle={handleDrawerToggle}
        />
        <CustomDrawer
          navItems={navItemsActive}
          mobileOpen={mobileOpen}
          handleDrawerToggle={handleDrawerToggle}
        />
      </Box>
      <Box component="main" sx={{ marginTop: 15 }}>
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
