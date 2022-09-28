import * as React from 'react';
import { Link } from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import { ListItemIcon, ListItemText } from '@mui/material';

const ITEM_HEIGHT = 48;

export default function HabitItemMenu({ habitId }: HabitItemMenuType) {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <IconButton
        aria-label="more"
        id="long-button"
        aria-controls={open ? 'long-menu' : undefined}
        aria-expanded={open ? 'true' : undefined}
        aria-haspopup="true"
        onClick={handleClick}
      >
        <MoreVertIcon />
      </IconButton>
      <Menu
        id="long-menu"
        MenuListProps={{
          'aria-labelledby': 'long-button',
        }}
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        PaperProps={{
          style: {
            maxHeight: ITEM_HEIGHT * 4.5,
          },
        }}
      >
        <Link to={`/record/${habitId}`} style={{ textDecoration: 'none' }}>
          <MenuItem onClick={handleClose}>
            <ListItemIcon sx={{ minWidth: 0, marginRight: 1 }}>
              <AutoGraphIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>기록</ListItemText>
          </MenuItem>
        </Link>
      </Menu>
    </div>
  );
}

interface HabitItemMenuType {
  habitId: number | undefined;
}
