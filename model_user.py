import pandas as pd
import re
"""
This class is the main class for users: customers and admins

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023
"""

class User:

    customer_role = "customer"
    admin_role = "admin"
    super_admin_role = "super_admin"
    default_user_id = "u_0000000000"
    default_user_name = "default_user"
    default_user_password = "password1"
    default_register_time = "00-00-0000_00:00:00"
    user_file_path = "data/users.txt"
    read_mode = "r"
    write_mode = "w"
    super_admin_uname = "super_user"
    user_id = "user_id"
    user_name = "user_name"
    user_password = "user_password"
    user_register_time = "user_register_time"
    user_role = "user_role"
    user_email = "user_email"
    user_mobile = "user_mobile"
#%%    
    def __init__(
        self,
        user_id: str = default_user_id,
        user_name: str = default_user_name,
        user_password: str = default_user_password,
        user_register_time: str =default_register_time,
        user_role: str = customer_role
    ):
        """
        This method initialises user object

        Parameters
        ----------
        user_id : str, optional
            DESCRIPTION. The default is default_user_id.
        user_name : str, optional
            DESCRIPTION. The default is default_user_name.
        user_password : str, optional
            DESCRIPTION. The default is default_user_password.
        user_register_time : str, optional
            DESCRIPTION. The default is default_register_time.
        user_role : str, optional
            DESCRIPTION. The default is customer_role.

        Returns
        -------
        None.

        """
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_register_time = user_register_time
        self.user_role = user_role
#%%        
    def __str__(self) -> str:
        """
        self: argument 

        Returns
        -------
        str
            dict of user object.

        """
        user_str = str(self.__dict__)
        return user_str
#%%        
    def read_return_list(
        self, 
        file_name:str,
        is_list_value_dict: bool = False,
        mode:str = read_mode
    )->list :
        """
        reads the file and returns it as a list of str or list of dict

        Parameters
        ----------
        file_name : str
            DESCRIPTION.
        is_list_value_dict : bool, optional
            DESCRIPTION. The default is False.
        mode : str, optional
            DESCRIPTION. The default is read_mode.

        Returns
        -------
        list
            DESCRIPTION.

        """
        
        with open(file_name,mode) as read_file:
            file_list = read_file.readlines()
        
        if not is_list_value_dict:
            return file_list
            
        if is_list_value_dict:
            for idx, line in enumerate(file_list):
                file_list[idx] = eval(line)
            return file_list
#%%
        
    def read_return_df(
        self,
        file_name:str
    ) -> pd.DataFrame :
        """
        reads the file and returns it as pandas dataframe

        Parameters
        ----------
        file_name : str
            DESCRIPTION.

        Returns
        -------
        file_df : TYPE
            DESCRIPTION.

        """
        
        file_list = self.read_return_list(file_name,is_list_value_dict = True)
        file_df = pd.DataFrame(file_list)
        return file_df
#%%    

    def append_to_file(
        self, 
        update_line:pd.DataFrame,
        file_name:str
    ) -> bool :
        """
        This method appends one new line existing file

        Parameters
        ----------
        file_name : str
            DESCRIPTION.
        update_line : pd.DataFrame
            DESCRIPTION.

        Returns
        -------
        bool
            returns True if append is succesful.

        """
        file_contents = self.read_return_df(file_name)
        updated_contents = pd.concat([file_contents,update_line], 
                                     ignore_index=True)
        return self.write_df_to_file(updated_contents,file_name)
    
#%%

    def write_df_to_file(
        self,
        df_to_write: pd.DataFrame,
        file_name:str,
        mode:str = write_mode
    ) -> bool :
        """
        This method writes the dataframe to file 

        Parameters
        ----------
        df_to_write : pd.DataFrame
            DESCRIPTION.
        file_name : str
            DESCRIPTION.
        mode : str, optional
            DESCRIPTION. The default is write_mode.

        Returns
        -------
        bool
            True if write is succesful else otherwise

        """
        
        try:
            df_to_write.fillna("Nil",inplace= True)
            write_list = df_to_write.to_dict('records')
            with open(file_name,mode,encoding='utf-8') as user_file:
                for data in write_list:
                    user_file.write(f"{str(data).strip()} \n")
            return True
        except:
            return False
#%%
    def search_return_df(
        self,
        search_term : str,
        is_user_name: bool,
        is_user_id: bool = False,
        is_search_list: bool = False
    ) -> pd.DataFrame :
        """
        searches for user_name or user_id returns one row or part of dataframe

        Parameters
        ----------
        search_term : str
            DESCRIPTION.
        is_user_name : bool
            DESCRIPTION.
        is_user_id : bool, optional
            DESCRIPTION. The default is False.
        is_search_list : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        return_df : TYPE
            DESCRIPTION.

        """
        
        user_file_df = self.read_return_df(User.user_file_path)
        if not is_search_list:
            if is_user_name : 
                try:
                    return_df =  user_file_df.loc[user_file_df[User.user_name] 
                                                  == search_term]
                except:
                    return_df = pd.DataFrame()
                return return_df    
            if is_user_id :
                try:
                    return_df =  user_file_df.loc[user_file_df[User.user_id] 
                                                  == search_term]
                except:
                    return_df = pd.DataFrame()
                return return_df
            
        if is_search_list:
            return_df = pd.DataFrame()
            return return_df
#%%