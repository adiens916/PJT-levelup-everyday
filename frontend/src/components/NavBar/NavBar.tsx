import React from 'react';
import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import CustomAppBar from './CustomAppBar/CustomAppBar';
import CustomDrawer from './CustomDrawer/CustomDrawer';

const navItems = ['Home', 'About', 'Contact'];

export default function NavBar() {
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <>
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
      </Box>
      <Box component="main" sx={{ marginTop: 15 }}>
        <Outlet />
      </Box>
    </>
  );
}

export interface NavBarType {
  navItems: string[];
  handleDrawerToggle: () => void;
  mobileOpen?: boolean;
}
