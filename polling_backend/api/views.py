from django.shortcuts import render
import mysql.connector as db
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from rest_framework import status 
from django.http import HttpResponseNotFound

from django.http import HttpResponseBadRequest

@api_view(['GET'])
def getUserData(re):
    try:
        mycon = db.connect(user='admin', password='20A25B0318', host='database-2.cx7du5eaphdp.us-east-1.rds.amazonaws.com', database='ap_survey')
        cursor=mycon.cursor()
        cursor.execute('call get_users();')
        result=cursor.fetchall()
        mycon.close()
        cursor.close()
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
        return Response(data)

    except Exception as e:
        
        
        return Response({"error": str(e)})


@api_view(['POST'])
def postUserData(request):
    try:
        all_data = request.data 
        print(all_data)
        data = [all_data[key] for key in all_data]
        print(data)

        c = db.connect(user='admin', password='20A25B0318', host='database-2.cx7du5eaphdp.us-east-1.rds.amazonaws.com', database='ap_survey')
        a = c.cursor()

        a.callproc('post_users', data)
        c.commit()

        a.close()
        c.close()

        return Response(status=status.HTTP_200_OK)

    except db.Error as e:
        print(f"Database Error: {e}")
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getSachivalayamData(re):
    try:
        mycon = db.connect(user='admin', password='20A25B0318', host='database-2.cx7du5eaphdp.us-east-1.rds.amazonaws.com', database='ap_survey')
        cursor=mycon.cursor()
        cursor.execute('call get_Sachivalayam();')
        result=cursor.fetchall()
        mycon.close()
        cursor.close()
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
        return Response(data)

    except Exception as e:
        
        
        return Response({"error": str(e)})

@api_view(['GET'])
def getMandalData(re):
    try:
        mycon = db.connect(user='admin', password='20A25B0318', host='database-2.cx7du5eaphdp.us-east-1.rds.amazonaws.com', database='ap_survey')
        cursor=mycon.cursor()
        cursor.execute('call get_Mandals();')
        result=cursor.fetchall()
        mycon.close()
        cursor.close()
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
        return Response(data)

    except Exception as e:
        
        
        return Response({"error": str(e)})


@api_view(['POST'])
def postMandalData(request):
    try:
        all_data = request.data 
        print(all_data)
        constituency = all_data['Constituency_name']
        mandal= all_data["Mandals_name"]
        print(mandal)
        data = [mandal,constituency]
        print(data)

        c = db.connect(user='admin', password='20A25B0318', host='database-2.cx7du5eaphdp.us-east-1.rds.amazonaws.com', database='ap_survey')
        a = c.cursor()

        a.callproc('post_Mandals', data)
        c.commit()

        a.close()
        c.close()

        return Response(status=status.HTTP_200_OK)

    except db.Error as e:
        print(f"Database Error: {e}")
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getDivisionData(re):
    try:
        mycon = db.connect(user='admin', password='20A25B0318', host='database-2.cx7du5eaphdp.us-east-1.rds.amazonaws.com', database='ap_survey')
        cursor=mycon.cursor()
        cursor.execute('call get_Mandals_division();')
        result=cursor.fetchall()
        mycon.close()
        cursor.close()
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
        return Response(data)

    except Exception as e:
        
        
        return Response({"error": str(e)})

@api_view(['GET'])
def getPartyData(re):
    try:
        with connection.cursor() as cursor:
            cursor.execute('call get_Parties()')
            result = cursor.fetchall()
            data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]

            return Response(data)
    except Exception as e:
        return Response({"error": str(e)})

@api_view(['POST'])
def postPartyData(request):
    try:
        all_data = request.data 
        print(all_data)
        number = all_data['serialNumber']
        party= all_data["name"]
        
        data = [party,number]
        print(data)
        c = db.connect(user='admin', password='20A25B0318', host='database-2.cx7du5eaphdp.us-east-1.rds.amazonaws.com', database='ap_survey')
        a = c.cursor()

        a.callproc('post_Parties(%s,%s)',data)
        c.commit()

        a.close()
        c.close()

        return Response(status=status.HTTP_200_OK)

    except db.Error as e:
        print(f"Database Error: {e}")
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def getVoters(re):
        try:
            with connection.cursor() as cursor:
                cursor.execute('call get_voters()')
                result = cursor.fetchall()
                data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]

                return Response(data)
        except Exception as e:
            return Response({"error": str(e)})



@api_view(['POST'])
def postSachivalayam(re):
    a=re.data
    dad=[a[key] for key in a]
    try:
        c=connection
        a=c.cursor()
        a.execute('call post_Sachivalayam(%s,%s,%s,%s)',dad)
        c.commit()
        a.close()
        c.close()
        return Response(status=status.HTTP_200_OK)
    except Exception:
        a.close()
        c.close()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_sach(request, pk):
    try:
      
        delete_query = 'CALL delete_Sachivalayam(%s);'
        params = (pk,)

        with connection.cursor() as cursor:
        
            cursor.execute(delete_query, params)

            if cursor.rowcount > 0:
                return Response(status=status.HTTP_200_OK)
            else:
                
                return HttpResponseNotFound('Record not found with the given id', status=404)

    except Exception as e:
        
        return HttpResponseBadRequest(f'Error: {str(e)}',status=400)



@api_view(["DELETE"])
def deleteMandal(request, pk):
    try:
      
        delete_query = 'CALL delete_Sachivalayam(%s);'
        params = (pk,)

        with connection.cursor() as cursor:
        
            cursor.execute(delete_query, params)

            if cursor.rowcount > 0:
                return Response(status=status.HTTP_200_OK)
            else:
                
                return HttpResponseNotFound('Record not found with the given id', status=404)

    except Exception as e:
        
        return HttpResponseBadRequest(f'Error: {str(e)}',status=400)



@api_view(["DELETE"])
def delete_division(request, pk):
    try:
        print(pk)
        delete_query = 'CALL delete_Mandal_Division(%s);'
        params = (pk,)

        with connection.cursor() as cursor:
        
            cursor.execute(delete_query, params)

            if cursor.rowcount > 0:
                return Response(status=status.HTTP_200_OK)
            else:
                
                return HttpResponseNotFound('Record not found with the given id', status=404)

    except Exception as e:
        
        return HttpResponseBadRequest(f'Error: {str(e)}',status=400)

@api_view(['GET'])
def getParts(re):
        try:
            with connection.cursor() as cursor:
                cursor.execute('call get_parts()')
                result = cursor.fetchall()
                data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]

                return Response(data)
        except Exception as e:
            return Response({"error": str(e)})

@api_view(['POST'])
def post_tiket(re):
    try:
        a = re.data
        mandal = [a[key] for key in a]
        
        c = connection
        a = c.cursor()
        a.execute('CALL Update_Voter_Details(%s,%s,%s,%s,%s,%s)', mandal)
        c.commit()
        a.close()
        c.close()
        return Response(status=status.HTTP_200_OK)

    except Exception as e:
        # Log the database error for debugging
        

        a.close()
        
        c.close()
        return Response(status=status.HTTP_400_BAD_REQUEST)





