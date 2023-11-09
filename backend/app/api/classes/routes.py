from flask_restx import Resource
from .models import class_model
from .namespace import api
from app.operations.class_operations import (
    add_class,
    get_class_by_id,
    get_all_classes,
    update_class,
    delete_class
)
from app.operations.message_operations import (
    get_class_messages,
    add_class_message
)
from app.api.class_groups.models import message_model, message_post_model
from app.decorators import require_authentication

@api.route('/')
class ClassList(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @api.marshal_list_with(class_model)
    def get(self):
        """List all classes"""
        return get_all_classes()

    @api.doc(security='apikey')
    @require_authentication("admin", "teacher")
    @api.expect(class_model)
    def post(self):
        """Create a new class"""
        return add_class(api.payload), 201

@api.route('/<int:class_id>')
@api.response(404, 'Class not found')
class ClassResource(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @api.marshal_with(class_model)
    def get(self, class_id):
        """Fetch a class given its identifier"""
        cls = get_class_by_id(class_id)
        if cls is None:
            api.abort(404, 'Class not found')
        return cls

    @api.doc(security='apikey')
    @require_authentication("admin", "teacher")
    @api.expect(class_model)
    @api.response(204, 'Class updated successfully')
    def put(self, class_id):
        """Update a class given its identifier"""
        update_class(class_id, api.payload)
        return None, 204

    @api.doc(security='apikey')
    @require_authentication("admin", "teacher")
    @api.response(204, 'Class deleted successfully')
    def delete(self, class_id):
        """Delete a class given its identifier"""
        delete_class(class_id)
        return None, 204

@api.route('/<int:class_id>/messages')
class ClassMessages(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @api.marshal_list_with(message_model)
    def get(self, class_id):
        """Get all messages for the main group of a specific class"""
        class_ = get_class_by_id(class_id)
        if not class_:
            api.abort(404, f'Class with id {class_id} not found')
        return get_class_messages(class_)

    @api.doc(security='apikey')
    @require_authentication()
    @api.expect(message_post_model)
    def post(self, class_id):
        """Post a new message to the main group of a specific class"""
        content = api.payload.get('content')
        message = add_class_message(content, class_id=class_id, user_id=user_id)
        if message:
            return api.marshal(message, message_model), 201
        api.abort(400, 'Could not add message to the class')