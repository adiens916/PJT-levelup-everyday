import React from 'react';
import { Link } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { NavBarType } from '../NavBar';

export default function CustomAppBar(props: NavBarType) {
  return (
    <AppBar component="nav">
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={props.handleDrawerToggle}
          sx={{ mr: 2, display: { sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>

        {/* By platform, display is changed  */}
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
        >
          MUI
        </Typography>
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
      </Toolbar>
    </AppBar>
  );
}
