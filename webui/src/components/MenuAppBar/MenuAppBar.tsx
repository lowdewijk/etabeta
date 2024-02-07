import * as React from 'react';
import {FC, ReactNode} from 'react';
import {useNavigate} from 'react-router-dom';
import {AccountCircle} from '@mui/icons-material';
import {
  AppBar,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
} from '@mui/material';

import {useLoggedInAuth} from '../../auth/AuthProvider';
import {ROUTE_SESSIONS} from '../../routes/Routes';

export type MenuAppBarProps = {
  parentPage?: ReactNode;
  pageName: string;
};

export const MenuAppBar: FC<MenuAppBarProps> = ({parentPage, pageName}) => {
  const {logout, username} = useLoggedInAuth();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const navigate = useNavigate();

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
          {parentPage || null}
          {parentPage ? ' / ' : null}
          {pageName}
        </Typography>
        <div>
          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem>Logged in as: {username}</MenuItem>
            <MenuItem
              onClick={() => {
                logout();
                handleClose();
                navigate(ROUTE_SESSIONS);
              }}
            >
              Logout
            </MenuItem>
          </Menu>
        </div>
      </Toolbar>
    </AppBar>
  );
};
