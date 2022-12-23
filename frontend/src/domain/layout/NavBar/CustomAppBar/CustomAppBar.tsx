import React from 'react';
import { Link } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import HomeIcon from '@mui/icons-material/Home';
import { NavBarType } from '../NavBar';

export default function CustomAppBar(props: NavBarType) {
  return (
    <AppBar component="nav">
      <Toolbar>
        <Box sx={{ flexGrow: 1 }}>
          <Link to="/">
            <IconButton edge="start">
              <HomeIcon sx={{ color: 'white' }} />
            </IconButton>
          </Link>
        </Box>

        <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
          {props.navItems.map((item) => (
            <Button key={item.name} sx={{ color: '#fff' }}>
              <Link
                to={item.link}
                onClick={item.onClick}
                style={{
                  textDecoration: 'none',
                  color: 'white',
                }}
              >
                {item.name}
              </Link>
            </Button>
          ))}
        </Box>

        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="end"
          onClick={props.handleDrawerToggle}
          sx={{ display: { sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}
