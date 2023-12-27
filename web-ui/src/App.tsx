import {memo} from 'react';
import {QueryClient, QueryClientProvider} from 'react-query';
import {HashRouter} from 'react-router-dom';
import {ToastContainer} from 'react-toastify';
import {createTheme, ThemeProvider} from '@mui/material/styles';

import AppGlobalStyles from 'src/AppGlobalStyles';
import {AppRoutes} from './routes/AppRoutes';

import 'react-toastify/dist/ReactToastify.css';

const theme = createTheme();

const queryClient = new QueryClient();

const App = (): JSX.Element => (
  <ThemeProvider theme={theme}>
    <HashRouter>
      <QueryClientProvider client={queryClient}>
        <AppGlobalStyles />
        <AppRoutes />
        <ToastContainer />
      </QueryClientProvider>
    </HashRouter>
  </ThemeProvider>
);

export default memo(App);
