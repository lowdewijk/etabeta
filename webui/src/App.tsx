import {memo} from 'react';
import {QueryClient, QueryClientProvider} from 'react-query';
import {HashRouter} from 'react-router-dom';
import {ToastContainer} from 'react-toastify';
import {createTheme, ThemeProvider} from '@mui/material/styles';

import AppGlobalStyles from 'src/AppGlobalStyles';
import {AuthProvider} from './auth/AuthProvider';
import {AppRoutes} from './routes/AppRoutes';

import 'react-toastify/dist/ReactToastify.css';

const theme = createTheme();

const queryClient = new QueryClient();

const App = (): JSX.Element => (
  <AuthProvider>
    <ThemeProvider theme={theme}>
      <HashRouter>
        <QueryClientProvider client={queryClient}>
          <AppGlobalStyles />
          <AppRoutes />
          <ToastContainer />
        </QueryClientProvider>
      </HashRouter>
    </ThemeProvider>
  </AuthProvider>
);

export default memo(App);
