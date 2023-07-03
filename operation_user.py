from model_user import User
from model_customer import Customer
from model_admin import Admin
import pandas as pd
import random
import time
"""
This class contains user opertations

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023
"""

class UserOperation:
#%%    
    def generate_unique_user_id(self) -> str:
        """
        generates and returns a unique user_id

        Returns
        -------
        str
            unique_user_id.

        """
        start = (10**(10-1))
        end = (10**10)-1
        temp_user_obj = User()
        flag = True
        while flag: 
            temp_user_id = "u_"+str(random.randint(start, end))
            user_data_df = temp_user_obj.read_return_df(temp_user_obj.user_file_path)
            try: 
                df_exist_user_id = pd.Series(user_data_df["user_id"])
            except KeyError : 
                df_exist_user_id = pd.Series([],dtype= "str")
            if temp_user_id not in df_exist_user_id.values:
                flag = False
                return temp_user_id
            else:
                flag = True
                continue
#%%
    def check_username_exist(self, user_name) -> bool:
        """
        This method checks if username alredy exists, if yes retrun True

        Parameters
        ----------
        user_name : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        temp_user_obj = User()
        user_data_df = temp_user_obj.read_return_df(temp_user_obj.user_file_path)
        try:
            df_exist_user_name = pd.Series(user_data_df["user_name"].apply(str.lower))
            if user_name.lower() in df_exist_user_name.values :
                return False
        except KeyError : 
            return True
        return True
#%%

    def validate_user_name(self, user_name:str) -> bool:
        """
        checks if username is over 5 char and contains only letter 
        and underscore

        Parameters
        ----------
        user_name : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        if len(user_name) < 5:
            return False
        for char in user_name : 
            if not (char.isalpha() or char == "_"):
                return False
        return True

#%% 

    def validate_password(self, user_password: str) -> bool:
        """
        checks if password is atleast 5 chars and atlest 1 alpha and 1 num

        Parameters
        ----------
        user_password : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        if len(user_password) < 5:
            return False
        if not any(char.isalpha() for char in user_password):
            return False
        if not any(char.isdigit() for char in user_password):
            return False
        return True
#%% 

    def encrypt_password(self,user_password:str) -> str:
        """
        Gives an encrypted password over two times length of orginal_password

        Parameters
        ----------
        user_password : str
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        str_len = 2*len(user_password)
        rand_str_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        rand_str = "".join(random.choice(rand_str_chars) 
                           for _ in range(str_len))
        encrypted_password = ""
        for i, char in enumerate(user_password):
            random_chars = rand_str[i*2:i*2+2]
            encrypted_password += random_chars + char
        return "^^"+encrypted_password+"$$"
#%%

    def return_time_str(self) -> str:
        """
        returns time_string of current time

        Returns
        -------
        str
            time_string of "%d-%m-%Y_%H:%M:%S" format

        """
        current_time = time.time()
        time_struct = time.localtime(current_time)
        # Format the time struct as string
        time_string = time.strftime("%d-%m-%Y_%H:%M:%S", time_struct)
        return time_string
#%%
    def decrypt_password(
        self,
        encrypted_password: str
    )-> str : 
        
        decrypted_passwd = ""
        encrypted_password = encrypted_password[2:-2]
        
        i = 2
        while i <= len(encrypted_password)-1:
            decrypted_passwd += encrypted_password[i]
            i+=3
        return decrypted_passwd
#%%            
    def login(
        self,
        user_name: str,
        user_password: str
    ) -> User :
        """
        logs in the user if credintials are correct then corresponding objects 
        are returned else default user object is returned 

        Parameters
        ----------
        user_name : str
            DESCRIPTION.
        user_password : str
            DESCRIPTION.

        Returns
        -------
        User
            DESCRIPTION.

        """
        
        tmp_user = User()
        login_df = tmp_user.search_return_df(user_name, is_user_name=True)
        
        if login_df.empty:
            return tmp_user
        if self.decrypt_password(login_df[User.user_password].item()) != user_password:
            return tmp_user
        
        if login_df[User.user_role].isin(
                [User.super_admin_role,User.admin_role]).bool() : 
            login_df_dict = login_df.to_dict("records")
            login_df_dict[0].pop(User.user_email,None)
            login_df_dict[0].pop(User.user_mobile)
            return Admin(**login_df_dict[0])
        
        if login_df[User.user_role].isin(
                [User.customer_role]).bool() : 
            login_df_dict = login_df.to_dict("records")
            return Customer(**login_df_dict[0])
#%%
    def pretty_print_object(
        self,
        print_obj : User
    ) -> str :
        
        if print_obj.user_role == User.customer_role : 
            message = ("\nProfile details are"
                       f"\nUser Name : {print_obj.user_name}"
                       f"\nAccount Active Since : {print_obj.user_register_time}"
                       f"\nEmail Id : {print_obj.user_email}"
                       f"\nMobile : {print_obj.user_mobile}")
            return message
        if print_obj.user_role in  (User.admin_role, User.super_admin_role) : 
            message = ("\nProfile details are"
                       f"\nUser Name : {print_obj.user_name}"
                       f"\nAccount Active Since : {print_obj.user_register_time}"
                       f"\nAdmin Role: {print_obj.user_role}")
            return message
#%%