import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import os

def app():
    # set title
    st.title('COVID19 Detector')
    # Create a text element and let the reader know the model is loading.
    model_load_state = st.text('Check server is alive')
    # Load model.
    r = requests.get('http://localhost:8000/alive', )
    if r.status_code != 200:
        raise ValueError ('server is down')
    # Notify the reader that the data was successfully loaded.
    model_load_state.text('Server is up, model loaded!')
    
    image = st.file_uploader("Upload an image for COVID Detection",type=["jpg", "png", "jpeg"])
    if image:
        st.image(image)
   
    st.session_state.disable_opt=False
    p=st.empty()    
    btn=p.button('Start Classification',disabled=st.session_state.disable_opt) 
        
    if btn:
        st.session_state.disable_opt=True
        # p.button('Start Classification',disabled=st.session_state.disable_opt)    
        if image:
            print(type(image))       
            data = {
                'image':image,
            }  
            response = requests.post('http://127.0.0.1:8000/predict', files=data)
            content=response.json()
            if response.status_code==200:      
                covid_prob, normal_prob = content['COVID19'], content['NORMAL']
                labels = ['COVID19', 'NORMAL']
                probs = [covid_prob, normal_prob]      
                fig = px.pie(labels, values = probs, names = labels)        
                fig.add_trace(go.Pie(labels=labels, values=probs,scalegroup='one', name="Gender",textposition='inside',showlegend=False,textinfo='label+percent'), 1, 1)
                st.plotly_chart(fig)       
                                    
            elif response.status_code!=200:
                st.error(content['error'])
                st.stop()
                            
        else:                                
            st.info('please upload image')



if __name__ == "__main__":
    # subprocess.Popen(['python', 'flask_api.py'])
    os.system('python flask_api.py &')
    app()

