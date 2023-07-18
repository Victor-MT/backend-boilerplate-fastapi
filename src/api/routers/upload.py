from fastapi import APIRouter, UploadFile, File, HTTPException, status, Response, Depends


def validate_file_format(file: UploadFile = File(...)):
    if not any(file.filename.__contains__(t) for t in ['.xlsx', '.xlsm']):
        raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                    detail="File format not suported. Try again with xlsx file type."
                )

router = APIRouter(
    prefix='/upload',
    tags=['upload'],
    dependencies=[Depends(validate_file_format)]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def updload( file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    media_type = file.content_type

    return Response(content, media_type=media_type, headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })
