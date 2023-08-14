from django import forms

class create_listing_form(forms.Form):
        title = forms.CharField(label='Title', initial=None, max_length=45, required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        'size': 30,
                                        'id': 'create-listing-title',
                                        'class': 'user-formfield',
                                        'placeholder': 'Enter a Catchy Title'
                                }))
        
        description = forms.CharField(label='Description', initial=None, max_length=255, required=True,
                                      widget=forms.Textarea(
                                          attrs={
                                                'id': 'create-listing-decription',
                                                'class': 'user-form-textarea',
                                                'placeholder': 'Give an accurate description of the item',
                                                'rows': 10,
                                                'cols': 55,
                                                'wrap': 'soft'
                                          }
                                      ))
        image_link = forms.URLField(label='Picture', initial=None, max_length=120, required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        'id': 'create-listing-image-link',
                                        'class': 'user-formfield',
                                        'placeholder': "Upload pic to imgur.com then copy paste 'Direct Link' here.",
                                        'size': 40,
                                        'autocomplete': 'Off',
                                    }
                                ))
        starting_bid= forms.FloatField(label='Start Bid', initial=None, required=True, min_value=1,
                                        widget=forms.NumberInput(
                                            attrs={
                                                'id': 'create-listing-starting_bid',
                                                'class': 'user-formfield create-listing-form-startbid',
                                                'placeholder': 'Low start Recommended',
                                                'size': 10,
                                            }
                                        ))

        category    = forms.CharField(label='Category', initial=None, max_length='16', required=True,
                                   widget=forms.TextInput(
                                       attrs={
                                              'id': 'create-listing-image-link',
                                              'class': 'user-formfield',
                                              'placeholder': '',
                                              'list': 'category_list'
                                       }
                            ))
        condition      = forms.CharField(label='Condition', initial=None, max_length='16', required=True,
                            widget=forms.TextInput(
                                attrs={
                                        'id': 'create-listing-image-link',
                                        'class': 'user-formfield',
                                        'placeholder': '',
                                        'list': 'conditions_list',
                                }
                            ))
        
        
        
class login_form(forms.Form):
        username = forms.CharField(label='Username', initial=None, max_length=45, required=True,
                            widget=forms.TextInput(
                                attrs={
                                    'autofocus': True,
                                    'id': 'login-form-title',
                                    'class': 'user-formfield',
                                    
                            }))
        
        password = forms.CharField(label='Password', initial=None, max_length=45, required=True,
                    widget=forms.PasswordInput(
                        attrs={
                            'id': 'login-form-password',
                            'class': 'user-formfield',
                            
                            
                    }))
        
        
        
        
        
        
class register_form(forms.Form):
        username = forms.CharField(label='Username', initial=None, max_length=45, required=True,
                                    widget=forms.TextInput(
                                        attrs={
                                            'autofocus': True,
                                            'id': 'register-form-username',
                                            'class': 'user-formfield', 
                                            'name': 'username',
                                    }))
        email = forms.CharField(label='Email', initial=None, max_length=45, required=True,
                                    widget=forms.EmailInput(
                                        attrs={
                                            'id': 'register-form-email',
                                            'class': 'user-formfield',
                                            'name': 'email',          
                                    }))
        
        password = forms.CharField(label='Password', initial=None, max_length=45, required=True,
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'id': 'register-form-password',
                                            'class': 'user-formfield', 
                                            'name': 'password'
                                    }))
        confirmation = forms.CharField(label='Confirm', initial=None, max_length=45, required=True,
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'id': 'register-form-password',
                                            'class': 'user-formfield', 
                                            'name': 'confirmation',
                                            'placeholder': 'Re-Type Password'
                                    }))
        
        
class bid_form(forms.Form):
        bid = forms.FloatField(label='', initial=None, min_value=1,
                             widget=forms.NumberInput(
                                 attrs={
                                     'id': 'bid-form-id',
                                     'class': 'bid-formfield',
                                     'name': 'form-bid',
                                 }
                             ))
        
class comment_form(forms.Form):
        user_comment = forms.CharField(label='', max_length=120, required=True,
                                      widget=forms.Textarea(
                                          attrs={
                                                'class': 'user-form-textarea comment-form-textarea',
                                                'rows': 3,
                                                'cols': 45,
                                          }
                                      ))
        




class listings_search_form(forms.Form):
    Category_Choices= [('All', 'All'), 
                       ('Furniture', 'Furniture'), 
                       ('Electronics', 'Electronics'), 
                       ('DIY', 'DIY'), 
                       ('Clothing', 'Clothing'), 
                       ('Games', 'Games'), 
                       ('Music', 'Music'),
                       ( 'Pets', 'Pets'), 
                       ('Art', 'Art'), 
                       ('Books', 'Books') ]
    
    category_choice= forms.ChoiceField(label='Categories', choices=Category_Choices,
                                     widget=forms.Select(attrs={
                                                'class': 'active-listings-dropdown',
                                                'id': 'category-select'
                                     }))
    

    Health_Choices= [('All','All'), ('New', 'New'), ('Mint', 'Mint'), ('Very-Good','Very-Good'), ('Good','Good'), ('Fair','Fair'), ('Broken','Broken')]
    health_choice= forms.ChoiceField(label='Condition', choices=Health_Choices,
                                     widget=forms.Select(attrs={
                                                'class': 'active-listings-dropdown',
                                                'id': 'health-select'
                                     }))
    
    
    Price_Choices= [('0', 'All'), ('0', '5'), ('1', '5-20'), ('2','20-50'), ('3','50-150'), ('4','150-350'), ('5','350-700'), ('6','700+'),('7','Pets')]
    price_choice= forms.ChoiceField(label='Price', choices=Price_Choices, 
                                     widget=forms.Select(attrs={
                                                   'class': 'active-listings-dropdown',
                                                    'id': 'price-select'
                                     }))
    
    Location_Choices= [('0','All'), ('0', '5 miles'), ('1', '10 miles'), ('2','50 miles'), ('3','National'), ('4','Europe'), ('5','N.America'), ('6','Worldwide')]
    location_choice= forms.ChoiceField(label='Locale', choices=Location_Choices, 
                                     widget=forms.Select(attrs={
                                                'class': 'active-listings-dropdown',
                                                'id': 'location-select',

                                     }))

    
    
    #Category_Choices= [('0', 'All'), ('1', 'Furniture'), ('2','Electronics'), ('3','DIY'), ('4','Clothing'), ('5','Games'), ('6','Music'),('7','Pets'), ('8','Art'), ('9','Books') ]
    #category_choice= forms.ChoiceField(label='Categories', 
    #                                 widget=forms.Select(attrs={
    #                                            'class': 'category_select',
    #                                            'onchange': 'this.form.submit();'     
    #                                 }),
    #                                 choices=Category_Choices, 
    #                                 )
    


class listing_auction_state_form(forms.Form):
    listing_states = [('All','All') , ('Active','Active') , ('Closed','Closed') ]
    listing_status = forms.ChoiceField(label='', widget=forms.RadioSelect, choices = listing_states)