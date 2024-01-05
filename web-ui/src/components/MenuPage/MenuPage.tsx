import {FC} from 'react';
import {Box} from '@mui/material';

import {MenuAppBar} from '../MenuAppBar/MenuAppBar';

export type MenuPageProps = {
  pageName: string;
  children: React.ReactNode;
};

export const MenuPage: FC<MenuPageProps> = ({pageName, children}) => {
  return (
    <Box
      sx={{
        height: '100vh',
        display: 'grid',
        gridTemplateAreas: `"header"
                            "main"`,
        gridTemplateColumns: '1fr ',
        gridTemplateRows: '3rem 1fr',
        gap: '1rem',
        '&> *': {
          backgroundColor: '#eee',
        },
      }}
    >
      <Box
        component="header"
        sx={{
          gridArea: 'header',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '0 0px',
        }}
      >
        <MenuAppBar pageName={pageName} />
      </Box>
      <Box
        component="main"
        sx={{
          gridColumn: 'main',
        }}
      >
        {children}
      </Box>
    </Box>
  );
};
