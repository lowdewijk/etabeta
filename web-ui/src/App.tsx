import {memo} from 'react';
import {BrowserRouter} from 'react-router-dom';
import {createTheme, ThemeProvider} from '@mui/material/styles';

import AppGlobalStyles from 'src/AppGlobalStyles';
import {AppRoutes} from './AppRoutes';

const theme = createTheme();

const App = (): JSX.Element => (
  <ThemeProvider theme={theme}>
    <BrowserRouter>
      <AppGlobalStyles />
      <AppRoutes />
    </BrowserRouter>
  </ThemeProvider>
);

export default memo(App);
