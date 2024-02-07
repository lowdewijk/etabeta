import {Navigate, Outlet} from 'react-router-dom';

import {useAuth} from '../auth/AuthProvider';

export const PrivateRoute = () => {
  const {isLoggedIn} = useAuth();

  // If authorized, return an outlet that will render child elements
  // If not, return element that will navigate to login page
  return isLoggedIn ? <Outlet /> : <Navigate to="/login" />;
};
