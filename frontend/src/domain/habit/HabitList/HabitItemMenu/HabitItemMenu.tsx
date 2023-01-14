import * as React from 'react';
import { Link } from 'react-router-dom';

import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import DeleteIcon from '@mui/icons-material/Delete';
import LowPriorityIcon from '@mui/icons-material/LowPriority';
import { ListItemIcon, ListItemText } from '@mui/material';

import { deleteHabit, updateImportance } from '../../api/crudApi';
import { HabitType } from '../../types';

const ITEM_HEIGHT = 48;

export default function HabitItemMenu({ habit }: HabitItemMenuType) {
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
        <Link to={`/record/${habit.id}`} style={{ textDecoration: 'none' }}>
          <MenuItem onClick={handleClose}>
            <ListItemIcon sx={{ minWidth: 0, marginRight: 1 }}>
              <AutoGraphIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>기록</ListItemText>
          </MenuItem>
        </Link>

        <MenuItem
          onClick={() => {
            const importance = prompt(
              `중요도에 따라 내림차순으로 정렬합니다. \n\n중요도를 설정해주세요.\n-범위   : 1 ~ 10000 (기본값: 100)\n-현재   : ${habit.importance}`,
            );
            if (importance && habit.id) {
              updateImportance(habit.id, Number(importance))
                .then(() => {
                  alert('설정 완료!');
                  location.reload();
                })
                .catch(() => {
                  alert('설정 실패...');
                });
            }
          }}
        >
          <ListItemIcon sx={{ minWidth: 0, marginRight: 1 }}>
            <LowPriorityIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>중요도</ListItemText>
        </MenuItem>

        <MenuItem
          onClick={() => {
            const isAgreed = confirm('해당 습관을 완전히 삭제하시겠습니까?');
            if (isAgreed && habit.id) {
              deleteHabit(habit.id)
                .then(() => {
                  alert('삭제 완료!');
                  location.reload();
                })
                .catch(() => {
                  alert('삭제 실패...');
                });
            }
          }}
        >
          <ListItemIcon sx={{ minWidth: 0, marginRight: 1 }}>
            <DeleteIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>삭제</ListItemText>
        </MenuItem>
      </Menu>
    </div>
  );
}

interface HabitItemMenuType {
  habit: HabitType;
}
