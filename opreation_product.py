import os 
import pandas as pd
from model_product import Product
from model_user import User
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#%%
"""
Product operation class to perform all product related options
Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 08-06-2023
Final date: 08-06-2023

"""



class ProductOperation:
    
    prod_csv_path = "data/product/"
    plot_path = "data/figure/"
    cols_read = Product.df_file_read_cols
    cols_final = Product.df_file_save_cols
    files = os.listdir(prod_csv_path)
    csv_files = [file for file in files if file.endswith('.csv')]
    final_csv_path = []
    for file in csv_files:
        file_path = os.path.join(prod_csv_path, file)
        final_csv_path.append(file_path)
        
#%%
    def extract_products_from_files(
        self
    ) -> None : 
        """
        Collects all products and writes in products.txt after dropping id

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        prod_df_list = [] 
        
        for path in ProductOperation.final_csv_path : 
            df = pd.read_csv(path)
            df_reqd = df.loc[:, df.columns.isin(ProductOperation.cols_read)]
            df_reqd = df_reqd[ProductOperation.cols_read]
            prod_df_list.append(df_reqd)
            
        pre_final_prod_df = pd.concat(prod_df_list,ignore_index=True)
        
        final_prod_df = pre_final_prod_df.drop_duplicates(subset="id")
        final_prod_df.columns = ProductOperation.cols_final
        final_to_write = final_prod_df.astype(str)
        final_to_write.fillna("Nil",inplace= True)
        write_list = final_to_write.to_dict('records')
        with open(Product.prod_file_path, 'w', encoding='utf-8') as f:
            for data in write_list : 
                f.write(f"{str(data).strip()} \n")
            
#%%
    def get_product_list(
        self,
        page_number: str
    ) -> tuple :
        """
        takes pagenumber as an argument and returns of tuple of objects

        Parameters
        ----------
        page_number : str
            DESCRIPTION.

        Returns
        -------
        tuple
            DESCRIPTION.

        """
        
        def product_obj(row) : 
            return Product(**row["prod_dict"])
        
        page_size = 10
        prod_file_df = Product().read_return_df(Product.prod_file_path)
        page_nums = np.arange(len(prod_file_df)) // page_size + 1
        prod_file_df["page_num"] = page_nums 
        max_pages = prod_file_df["page_num"].max()
        page_number = int(page_number)
        return_df = prod_file_df.query("page_num == @page_number")
        return_df = return_df.drop("page_num",axis = 1)
        prod_df_dict = return_df.to_dict("records")
        prod_return_df = pd.DataFrame()
        prod_return_df["prod_dict"] = prod_df_dict
        prod_return_df["prod_obj"] = prod_return_df.apply(
            product_obj,axis = 1)
        
        prod_return_df = prod_return_df.drop("prod_dict",axis = 1)
        return_prod_list = prod_return_df["prod_obj"].to_list()
        return_tuple = (return_prod_list,page_number,max_pages)
        return return_tuple
#%%
    
    def delete_product(
        self,
        product_id:str
    ) -> bool :
        """
        checks if product_id exists then deletes it accordingly

        Parameters
        ----------
        product_id : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        prod_find = Product().search_return_prod_df(search_term = product_id, 
                                                    is_prod_id = True, 
                                                    is_name_keyword = False)
        if prod_find.empty :
            return False
        
        prod_file_df = Product().read_return_df(Product.prod_file_path) 
        prod_file_df = prod_file_df.drop(prod_find.index)
        return Product().write_df_to_file(prod_file_df, Product.prod_file_path)        
#%% 

    def get_product_list_by_keyword(
        self,
        keyword
    ) -> tuple() : 
        """
        finds key word in product name and returns tuple containing product 
        objects

        Parameters
        ----------
        keyword : TYPE
            DESCRIPTION.

        Returns
        -------
        tuple
            DESCRIPTION.

        """
        
        prod_find = Product().search_return_prod_df(search_term = keyword, 
                                                    is_prod_id = False, 
                                                    is_name_keyword = True)
        
        prod_df_dict = prod_find.to_dict("records")
        prod_return_df = pd.DataFrame()
        prod_return_df["prod_dict"] = prod_df_dict
        prod_return_df["prod_obj"] = prod_return_df.apply(
            ProductOperation.product_obj,axis = 1)
        
        prod_return_df = prod_return_df.drop("prod_dict",axis = 1)
        return_prod_list = prod_return_df["prod_obj"].to_list()
        return_tuple = (return_prod_list,"N/A","N/A")
        return return_tuple
#%%

    def product_obj(row) : 
        return Product(**row["prod_dict"])
#%%    
    
    def get_product_by_id(
        self,
        product_id: str
    ) -> tuple():   
        """
        searches product by id returns tuple containing product object

        Parameters
        ----------
        product_id : str
            DESCRIPTION.

        Returns
        -------
        tuple
            DESCRIPTION.

        """
        
        prod_find = Product().search_return_prod_df(search_term = product_id, 
                                                    is_prod_id = True, 
                                                    is_name_keyword = False)
        
        prod_df_dict = prod_find.to_dict("records")
        prod_return_df = pd.DataFrame()
        prod_return_df["prod_dict"] = prod_df_dict
        prod_return_df["prod_obj"] = prod_return_df.apply(
            ProductOperation.product_obj,axis = 1)
        
        prod_return_df = prod_return_df.drop("prod_dict",axis = 1)
        return_prod_list = prod_return_df["prod_obj"].to_list()
        return_tuple = (return_prod_list,"N/A","N/A")
        return return_tuple
#%%   

    def delete_all_products(
        self
    )-> None:
        """
        Writes an empty df to products.txt

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        del_final = pd.DataFrame()
        del_flag = Product().write_df_to_file(del_final, Product.prod_file_path)
#%%   

    

    def generate_category_figure(self): 
        """
        plots and saves category data

        Returns
        -------
        None.

        """
        try :
            df = Product().read_return_df(is_string= False)
            category_counts = df['prod_category'].value_counts().sort_values(
                ascending=False)
            
            colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                      "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
            # Create a bar chart
            plt.figure(figsize=(11, 7))
            category_counts.plot(kind='bar',color = colors)
        
            # Set labels and title
            plt.xlabel('Category')
            plt.ylabel('Number of Products')
            plt.title('Total Number of Products by Category')
        
            # Save the figure to the data/figure folder
            plt.savefig('data/figure/generate_category_figure.png')
            plt.close()
            
            return True
        except : pass
#%%

    def generate_discount_figure(self):
        """
        pie chart for all discounted figures

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        try : 
            df = Product().read_return_df(is_string= False)
            less_30 = df[df["prod_discount"] < 30].shape[0]
            between_30_and_60 = df[(df["prod_discount"] >= 30) & (df["prod_discount"] <= 60)].shape[0]
            above_60 = df[df["prod_discount"] > 60].shape[0]
        
            discount_counts = [less_30, between_30_and_60, above_60]
        
            # Define labels for the pie chart
            labels = ['< 30', '30 - 60', '> 60']
        
            # Set colors for the pie chart
            colors = ["#FFD700", "#32CD32", "#FF7F50"]
        
            plt.figure(figsize=(10, 10))
            plt.pie(discount_counts, labels=labels, colors=colors)
            plt.title("Proportion of Products by Discount Percentage")
        
            # Save the figure to the data/figure folder
            plt.savefig("data/figure/generate_discount_figure.png")
            plt.close()
            return True 
        except : 
            return False
   
    
#%%
    def generate_likes_discount_scatter(self):
        """
        scatter plot for likes and discount

        Returns
        -------
        None.

        """
        
        try : 
            df = Product().read_return_df(is_string= False)
            likes_count = df["prod_likes_count"]
            discount = df["prod_discount"]
            
            colors = ["#FF0000"]
            # Create a scatter plot
            plt.figure(figsize=(11, 7))
            plt.scatter(discount, likes_count, alpha=0.4,color = colors)
            plt.xlabel("Discount")
            plt.ylabel("Likes Count")
            plt.title("Scatter Chart - Likes Count vs Discount")
        
            # Save the figure to the data/figure folder
            plt.savefig("data/figure/generate_likes_discount_scatter.png")
            plt.close()
            return True
        except : 
            return False
#%%
    def generate_likes_count_chart(self):
        """
        In this method I choose a horizontal bar chart and it is plotted in k

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        df = Product().read_return_df(is_string= False)
        
        try : 
            filtered_df = df[["prod_category", "prod_likes_count"]]

            category_likes_sum = filtered_df.groupby(
                "prod_category")["prod_likes_count"].sum().sort_values()
            
            colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                      "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
            plt.figure(figsize=(11, 7))
            plt.barh(category_likes_sum.index, category_likes_sum.values,color = colors)
            plt.xlabel("Likes Count in 1000s")
            plt.ylabel("Category")
            plt.title("Sum of Likes Count by Category")
            formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x / 1000))
            plt.gca().xaxis.set_major_formatter(formatter)
            plt.savefig("data/figure/generate_likes_count.png")
            plt.close()
            return True
        except: 
            return False
#%%        