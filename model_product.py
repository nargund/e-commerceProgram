import random
import string
import pandas as pd

"""
Product class 

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 07-06-2023
Final date: 07-06-2023

"""

class Product:
    
    prod_id = "prod_id"
    prod_model = "prod_model"
    prod_category = "prod_category"
    prod_name = "prod_name"
    prod_current_price = "prod_current_price"
    prod_raw_price = "prod_raw_price"
    prod_discount = "prod_discount"
    prod_likes_count = "prod_likes_count"
    df_file_save_cols = [prod_id,prod_model,prod_category,prod_name,
                    prod_current_price,prod_raw_price,prod_discount,
                    prod_likes_count]
    df_file_read_cols = ["id","model","category","name","current_price",
                         "raw_price","discount","likes_count"]
    prod_file_path = "data/products.txt"
    write_mode = "w+"
    read_mode = "r"
    
    def __init__(
        self,
        prod_id: str = "",
        prod_model: str = "",
        prod_category: str = "",
        prod_name: str = "",
        prod_current_price: str = "",
        prod_raw_price: str = "",
        prod_discount: str = "",
        prod_likes_count: str = ""        
    ) : 
        self.prod_id = prod_id
        self.prod_model = prod_model
        self.prod_category = prod_category
        self.prod_name = prod_name
        self.prod_current_price = prod_current_price
        self.prod_raw_price = prod_raw_price
        self.prod_discount = prod_discount
        self.prod_likes_count = prod_likes_count
        
#%%

    def __str__(self) : 
        
        return str(self.__dict__)
    
#%%

    def read_return_df(
        self,
        prod_file_path: str = prod_file_path,
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
        prod_file_path : str
            DESCRIPTION.
        mode : str, optional
            DESCRIPTION. The default is "r".

        Returns
        -------
        file_df : TYPE
            DESCRIPTION.

        """
        
        with open(prod_file_path,mode,encoding="utf-8") as read_file:
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
                for column in file_df.columns:
                    try:
                        file_df[column] = pd.to_numeric(file_df[column])
                    except ValueError:
                        pass
                file_df[Product.prod_id] = file_df[Product.prod_id].apply(str)
                return file_df
            except: 
                return pd.DataFrame()
#%%
    
    def search_return_prod_df(
        self,
        search_term: str,
        is_prod_id: bool,
        is_name_keyword: bool
    ) -> pd.DataFrame :
        """
        takes search term and if product id does exact match and returns df
        if name does contains match
        
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
        
        
        prod_file_df = self.read_return_df(Product.prod_file_path)
        
        
        if is_prod_id : 
            try:
                return_df =  prod_file_df.query("prod_id == @search_term")
            except:
                return_df = pd.DataFrame()
            return return_df
        
        if is_name_keyword : 
            try:  
                return_df = prod_file_df[
                prod_file_df["prod_name"].str.contains(search_term, 
                                                       case=False)]
               
            except: 
                return_df = pd.DataFrame()
                
            return return_df
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
