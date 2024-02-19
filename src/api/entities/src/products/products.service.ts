import { Injectable } from '@nestjs/common';
import { PrismaClient} from '@prisma/client';

@Injectable()
export class ProductsService {
    private prisma = new PrismaClient();

    async getAllProducts(){
        try {
            return await this.prisma.products.findMany(); // Adjusted to 'products'
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async getProductById(id: string) {
        try {
            return await this.prisma.products.findUnique({ // Adjusted to 'products'
                where: { id }
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async createProduct(productData: any) {
        try {
            return await this.prisma.products.create({ // Adjusted to 'products'
                data: productData
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async updateProduct(id: string, productData: any) {
        try {
            return await this.prisma.products.update({ // Adjusted to 'products'
                where: { id },
                data: productData
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async deleteProduct(id: string) {
        try {
            return await this.prisma.products.delete({ // Adjusted to 'products'
                where: { id }
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }
}
