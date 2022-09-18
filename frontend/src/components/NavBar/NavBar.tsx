import React from 'react';
import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import CustomAppBar from './CustomAppBar/CustomAppBar';
import CustomDrawer from './CustomDrawer/CustomDrawer';

export interface NavBarType {
  navItems: string[];
  handleDrawerToggle: () => void;
  mobileOpen?: boolean;
}

export default function NavBack() {
  return (
    <>
      <DrawerAppBar />
      <Outlet />
    </>
  );
}

const navItems = ['Home', 'About', 'Contact'];

export function DrawerAppBar() {
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CustomAppBar
        navItems={navItems}
        handleDrawerToggle={handleDrawerToggle}
      />
      <CustomDrawer
        navItems={navItems}
        mobileOpen={mobileOpen}
        handleDrawerToggle={handleDrawerToggle}
      />
      <Box component="main" sx={{ p: 3 }}></Box>
    </Box>
  );
}
