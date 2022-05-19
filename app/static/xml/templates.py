from sre_constants import SUCCESS

SUCCESS = """
        <cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
            <cas:authenticationSuccess>
                <cas:user>{email}</cas:user>
                <cas:attributes>
                    <cas:user_id>{_id}</cas:user_id>
                    <cas:email>{email}</cas:email>
                    <cas:phone/>
                    <cas:fullname/>
                    <cas:token>{token}</cas:token>
                </cas:attributes>
            </cas:authenticationSuccess>
        </cas:serviceResponse>
    """