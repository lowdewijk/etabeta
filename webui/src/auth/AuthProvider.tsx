import {createContext, FC, useContext, useState} from 'react';

export type AuthContextProps = {
  login: (username: string) => void;
  logout: () => void;
  isLoggedIn: boolean;
  username?: string;
};

const AuthContext = createContext<AuthContextProps>({
  login: () => {},
  logout: () => {},
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

  return (
    <AuthContext.Provider value={{isLoggedIn, username, login, logout}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
