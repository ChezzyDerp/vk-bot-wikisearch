import wikipedia, random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

wikipedia.set_lang('ru')


token = 'your token'

vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)



def write_msg(user_id, message):

    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id':random.randint(1,100000)})



def getResponse(request, id):
    number = 0
    response = ''
    answer = 0
    indexRequest = 0

    for i in request:
        indexRequest += 1
        response = response + '['+str(indexRequest)+'] - '+ i + '\n'

    write_msg(id, response)

    for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:

                    response = ''

                    for i in request:
                            
                        try:
                            number = int(event.text)
                            if number == (request.index(i) + 1):
                                
                                response = i

                                write_msg(event.user_id, wikipedia.summary(response))

                                main()
                            break      

                        except wikipedia.exceptions.WikipediaException as e:
                            write_msg(event.user_id, 'Вы ввели слишком большое количство сиволов. (макс 300)')
                            main()
                            break

                        except ValueError:
                            write_msg(event.user_id, 'Упс, похоже вы ввели не цифру, а символ :)')
                            write_msg(event.user_id, 'Введите название статьи')
                            main()
                            break
                                   

def main():
   
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            

            if event.to_me:

                response = event.text

                response2 = wikipedia.search(response)
                
                getResponse(response2, event.user_id)

main()    



