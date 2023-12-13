import {memo} from 'react';
import {QueryClient, QueryClientProvider} from 'react-query';
import {BrowserRouter} from 'react-router-dom';
import {createTheme, ThemeProvider} from '@mui/material/styles';

import AppGlobalStyles from 'src/AppGlobalStyles';
import {AppRoutes} from './AppRoutes';

const theme = createTheme();

const queryClient = new QueryClient();

const App = (): JSX.Element => (
  <ThemeProvider theme={theme}>
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <AppGlobalStyles />
        <AppRoutes />
      </QueryClientProvider>
    </BrowserRouter>
  </ThemeProvider>
);

export default memo(App);
