from model_user import User 
import pandas as pd
import time
import random 

"""
Product operation class to perform all product related options
Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 08-06-2023
Final date: 08-06-2023
"""
#%%

class Order: 
    
    order_id = "order_id"
    user_id = "user_id"
    order_time = "order_time"
    prod_id = "prod_id"
    write_mode = "w+"
    read_mode = "r"
    order_file_path = "data/orders.txt"
    
    default_user_id = User.default_user_id
    default_prod_id = ""
    default_order_time = User.default_register_time
    default_order_id = "o_000000"

    def __init__(
        self,
        order_id: str = default_order_id,
        user_id: str = default_user_id,
        prod_id: str = default_order_id,
        order_time: str = default_order_time
    ) : 
        
        self.order_id = order_id
        self.user_id = user_id 
        self.prod_id = prod_id
        self.order_time = order_time
        
#%%
    
    def __str__(
        self
    )  : 
        
        order_str = self.__dict__
        return str(order_str)
    
#%% 

    def write_df_to_file(
        self,
        df_to_write: pd.DataFrame,
        file_name:str = order_file_path,
        mode:str = write_mode
    ) -> bool :
        """
        This method writes the dataframe to file 

        Parameters
        ----------
        df_to_write : pd.DataFrame
            DESCRIPTION.
        file_name : str, optional
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
        search_term: str,
        is_order_id: bool,
        is_cust_id: bool
    ) -> pd.DataFrame :
        """
        takes search term and if is_order id does exact match and returns df
        same for is_cust_id
        
        Parameters
        ----------
        search_term : str
            DESCRIPTION.
        is_prod_id : bool
            DESCRIPTION.
        is_name_keyword : bool
            DESCRIPTION.

        Returns
        -------
        return_df : TYPE
            DESCRIPTION.

        """
        
        
        order_file_df = self.read_return_df(Order.order_file_path)
        
        
        if is_order_id : 
            try:
                return_df =  order_file_df.query("order_id == @search_term")
            except:
                return_df = pd.DataFrame()
            return return_df
        
        if is_cust_id : 
            try:  
                return_df = order_file_df.query("user_id == @search_term")
            except: 
                return_df = pd.DataFrame()
                
            return return_df    
#%%

    def read_return_df(
        self,
        order_file_path: str = order_file_path,
        is_string: bool = True,
        mode:str = read_mode
    ) -> pd.DataFrame : 
        """
        takes filename as argument and returns a df with appropiate
        data types
        if is_string is false is True returns dataframe with appropiate numeric 
        conversion
        if file is empty returns empty df 

        Parameters
        ----------
        prod_file_path : str, optional
            DESCRIPTION.
        mode : str, optional
            DESCRIPTION. The default is "r".

        Returns
        -------
        file_df : TYPE
            DESCRIPTION.

        """
        
        with open(order_file_path,mode,encoding="utf-8") as read_file:
            file_list = read_file.readlines()
            
        for idx, line in enumerate(file_list):
            file_list[idx] = eval(line)
            
        file_df = pd.DataFrame(file_list)
        file_df = file_df.convert_dtypes()
        
        if file_df.empty : 
            return pd.DataFrame()
        
        if is_string :        
            return file_df
        
        if not is_string : 
            try : 
                file_df["order_time"] = pd.to_datetime(file_df["order_time"], 
                                                       format="%d-%m-%Y_%H:%M:%S")                      
            except: 
                pass
            
            return file_df
#%%
    def append_to_file(
        self, 
        update_line:pd.DataFrame,
        file_name:str = order_file_path
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
    def current_time_str(
        self ) -> str : 
        """
        generates a current_time str

        Returns
        -------
        str
            DESCRIPTION.

        """
        current_time = time.time()
        time_struct = time.localtime(current_time)
        # Format the time struct as string
        time_string = time.strftime("%d-%m-%Y_%H:%M:%S", time_struct)
        return time_string
#%%

    def random_time_str (
        self 
    ) -> str: 
        
        start_date = pd.Timestamp.now() - pd.DateOffset(months=12)
        end_date = pd.Timestamp.now()
        random_datetime = pd.to_datetime(random.uniform(start_date.value, end_date.value))
        random_datetime_str = random_datetime.strftime("%d-%m-%Y_%H:%M:%S")
        return random_datetime_str
    
#%%    
        
        
    
    