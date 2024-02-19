import { Injectable } from '@nestjs/common';
import { PrismaClient} from '@prisma/client';

@Injectable()
export class OrdersService {
    private prisma = new PrismaClient();

    async getAllOrders() {
        try {
            return await this.prisma.orders.findMany(); // Adjusted to 'orders'
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async getOrderById(id: string) {
        try {
            return await this.prisma.orders.findUnique({ // Adjusted to 'orders'
                where: { id }
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async createOrder(orderData: any) {
        try {
            return await this.prisma.orders.create({ // Adjusted to 'orders'
                data: orderData
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async updateOrder(id: string, orderData: any) {
        try {
            return await this.prisma.orders.update({ // Adjusted to 'orders'
                where: { id },
                data: orderData
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async deleteOrder(id: string) {
        try {
            return await this.prisma.orders.delete({ // Adjusted to 'orders'
                where: { id }
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }
}
