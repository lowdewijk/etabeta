import {createContext, FC, useContext, useState} from 'react';

export type AuthContextLoggedOutProps = {
  login: (username: string) => void;
  isLoggedIn: false;
  username: undefined;
};

export type AuthContextLoggedInProps = {
  logout: () => void;
  isLoggedIn: true;
  username: string;
};

export type AuthContextProps =
  | AuthContextLoggedOutProps
  | AuthContextLoggedInProps;

const AuthContext = createContext<AuthContextProps>({
  login: () => {},
  isLoggedIn: false,
  username: undefined,
});

export type AuthProviderProps = {
  children: React.ReactNode;
};

export const AuthProvider: FC<AuthProviderProps> = ({children}) => {
  const [username, setUsername] = useState(
    localStorage.getItem('user') || undefined,
  );

  const login = (uname: string) => {
    localStorage.setItem('user', uname);
    setUsername(uname);
  };

  const logout = () => {
    localStorage.removeItem('user');
    const x = undefined;
    setUsername(x);
  };

  const isLoggedIn = !!username;

  const props: AuthContextProps = isLoggedIn
    ? {
        logout,
        username,
        isLoggedIn: true,
      }
    : {
        login,
        username: undefined,
        isLoggedIn: false,
      };

  return <AuthContext.Provider value={props}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextProps => {
  return useContext(AuthContext);
};

export const useLoggedInAuth = (): AuthContextLoggedInProps => {
  const result = useAuth();
  if (!result.isLoggedIn) {
    throw new Error('You must be authenticated to use this function.');
  }
  return result;
};

export const useLoggedOutAuth = (): AuthContextLoggedOutProps => {
  const result = useAuth();
  if (result.isLoggedIn) {
    throw new Error('You must not be authenticated to use this function.');
  }
  return result;
};
